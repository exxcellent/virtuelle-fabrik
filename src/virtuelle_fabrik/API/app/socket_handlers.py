from enum import Enum
from attr import asdict, define
from fastapi import FastAPI
import socketio
import asyncio
from virtuelle_fabrik.domain.models import Produktionslinie, Station

from virtuelle_fabrik.persistence.produktionslinien import (
    get_produktionslinie,
    udpate_produktsionslinie,
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
    title: str | None = None
    details: str | None = None
    type: NotificationType | None = None
    showClose: bool | None = None


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
        await self.emit("produktionslinieChanged", asdict(await get_produktionslinie()))

    def on_disconnect(self, sid):
        pass

    async def on_changeProduktionslinie(self, sid, produktionslineDto: dict):
        produktionslinie = Produktionslinie(
            id="1",
            stationen=[Station(**s) for s in produktionslineDto["stationen"]],
            chargen=[],
            mitarbeiter=[],
        )

        await udpate_produktsionslinie(produktionslinie)
        await self.emit("produktionslinieChanged", produktionslineDto, skip_sid=sid)

    async def on_validateProduktionslinie(
        self, sid, produktionslinie
    ) -> list[EditorNotification]:
        # TODO: actually validate incoming produktionslinie
        return []

    async def on_startSimulation(self, sid, produktionslinieDto: dict):
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
