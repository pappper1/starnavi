from fastapi import APIRouter, Depends, Response


router = APIRouter(
	prefix="/comment",
	tags=["Comments"],
)
