from API.app.src.domain.models import Produktionslinie


holder = dict(
    produktionslinie=Produktionslinie(
        id="1",
        stationen=[],
        chargen=[],
        mitarbeiter=[],
    )
)


async def get_produktionslinie() -> Produktionslinie:
    # TODO: Produktionslinie aus Datenbank beziehen
    return holder["produktionslinie"]


async def udpate_produktsionslinie(produktionsline: Produktionslinie):
    # TODO: Produktionslinie in Datenbank persistieren
    holder["produktionslinie"] = produktionsline
