from fastapi import APIRouter, Depends, Response


router = APIRouter(
	prefix="/post",
	tags=["Posts"],
)
