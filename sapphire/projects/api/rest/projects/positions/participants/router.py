import fastapi

from . import handlers, review

router = fastapi.APIRouter()

router.add_api_route(
    path="/", methods=["POST"], endpoint=handlers.create_participant,
)
router.add_api_route(
    path="/{participant_id}", methods=["GET"], endpoint=handlers.get_participant,
)
router.add_api_route(
    path="/{participant_id}", methods=["POST"], endpoint=handlers.update_participant,
)
router.include_router(review.router, prefix="/{participant_id}/review")
