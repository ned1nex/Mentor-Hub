from fastapi.routing import APIRouter

from .modules.clients.router import router as clients_router
from .modules.mentors.router import router as mentors_router
from .modules.requests.router import router as requests_router
from .modules.stats.router import router as stats_router
from .modules.support.router import router as support_router
from .modules.admins.router import router as admin_router

global_router = APIRouter()

global_router.include_router(clients_router)
global_router.include_router(mentors_router)
global_router.include_router(requests_router)
global_router.include_router(support_router)
global_router.include_router(stats_router)
global_router.include_router(admin_router)