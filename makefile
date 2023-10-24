.PHONY: prisma db dev

prisma:
	prisma db push

dev:
	uvicorn main:app --host 0.0.0.0 --port 8000
