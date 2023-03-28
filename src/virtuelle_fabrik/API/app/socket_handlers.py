from enum import Enum
from typing import List
import uuid
from attr import asdict, define
from fastapi import FastAPI
import socketio
import asyncio

from virtuelle_fabrik.domain.models import Produktionslinie, Station

from virtuelle_fabrik.persistence.charge import get_charge
from virtuelle_fabrik.persistence.database import async_session
from virtuelle_fabrik.persistence.maschinen import get_maschine
from virtuelle_fabrik.persistence.produktionslinien import (
    add_produktionslinie,
    update_produktionslinie,
)


class NotificationType(str, Enum):
    ERROR = "Error"
    WARN = "Warn"
    SUCCESS = "Success"
    INFO = "Info"


@define
class EditorNotification:
    title: str | None = None
    id: str | None = None
    details: str | None = None
    type: NotificationType | None = None
    showClose: bool | None = None


@define
class StationTO:
    id: str
    name: str
    maschinen: List[str]
    chargen: List[str]


@define
class ProduktionslinieTO:
    id: str
    stationen: List[StationTO]


def convert_to_produktionslinieto(
    produktionslinie: Produktionslinie,
) -> ProduktionslinieTO:
    return ProduktionslinieTO(
        id=produktionslinie.id,
        stationen=[
            StationTO(
                id=x.id,
                name=x.name,
                maschinen=list([m.id for m in x.maschinen]),
                chargen=list([c.id for c in x.chargen]),
            )
            for x in produktionslinie.stationen
        ],
    )


class EditorNamespace(socketio.AsyncNamespace):
    _task: asyncio.Task | None = None

    async def run_optimization(self):
        # TODO: Actually do some optimization stuff
        simulation_id = "1"

        await self.emit("simulationRunning", simulation_id)
        await asyncio.sleep(5)
        await self.emit(
            "simulationFinished",
            data=(
                simulation_id,
                asdict(
                    EditorNotification(
                        details="Die simulation lief ganz wunderbar und "
                        + "es gibt nichts zu beanstanden! Priorität "
                        + "kann medium oder low sein",
                        type=NotificationType.SUCCESS,
                    )
                ),
            ),
        )

    async def on_connect(self, sid, environ):
        async with async_session() as session:
            await self.emit(
                "produktionslinieChanged",
                convert_to_produktionslinieto(
                    await add_produktionslinie(
                        session, Produktionslinie(id=uuid.uuid4().hex)
                    )
                ),
            )

    def on_disconnect(self, sid):
        pass

    async def on_changeProduktionslinie(
        self, sid, produktionslineto: ProduktionslinieTO
    ):
        async with async_session() as session:

            def synchronous_get_all(getter, list):
                results = [getter(session, x) for x in list]
                return asyncio.gather(*results)

            produktionslinie = Produktionslinie(
                id=produktionslineto.id,
                stationen=[
                    Station(
                        id=s.id,
                        name=s.name,
                        maschinen=synchronous_get_all(get_maschine, s.maschinen),
                        chargen=synchronous_get_all(get_charge, s.chargen),
                    )
                    for s in produktionslineto.stationen
                ],
            )

            await update_produktionslinie(produktionslinie)
            await self.emit("produktionslinieChanged", produktionslineto, skip_sid=sid)

    async def on_validateProduktionslinie(
        self, sid, produktionslinie
    ) -> list[EditorNotification]:
        # TODO: actually validate incoming produktionslinie
        return []

    async def on_startSimulation(self, sid, produktionslinieto: ProduktionslinieTO):
        if self._task and not self._task.cancelled():
            self._task.cancel()

        asyncio.create_task(self.run_optimization())

    async def on_cancelSimulation(self, sid):
        if not self._task:
            return

        cancelled = self._task.cancel()

        if cancelled:
            await self.emit("simulationCanceled")


def setupWebsocket(app: FastAPI):
    sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
    _app = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")
    app.mount("/ws", _app)
    app.sio = sio

    sio.register_namespace(EditorNamespace("/szenarios/1/editor/"))
