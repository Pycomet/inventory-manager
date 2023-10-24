# CRUD OPERATIONS
import aioredis
from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime
from contextlib import asynccontextmanager


# ADD MESSAGING QUEUE 
# Initialize Redis connection
async def get_redis():
    redis = await aioredis.create_redis_pool('redis://localhost')
    yield redis
    redis.close()
    await redis.wait_closed()

# Function to push product ID to queue
async def push_product_to_queue(product_id: int):
    async with get_redis() as redis:
        await redis.lpush('product_queue', product_id)

# Function to consume product queue
async def consume_product_queue():
    while True:
        async with get_redis() as redis:
            product_id = await redis.brpop('product_queue', timeout=5)
            if product_id:
                product_id = int(product_id[1])
                # Process product with ID product_id
            else:
                pass




# Create an async context manager for handling Prisma connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()



app = FastAPI(
    title="Inventory Manager API",
    version="1.0.0",
    lifespan=lifespan,
    redoc_url="/redoc",
    description="This project is a simple Inventory Management System for an e-commerce platform. It supports basic CRUD operations for managing items in inventory and is designed to handle a high volume of concurrent read and write operations."
)

# Initialize Prisma
prisma = Prisma()

# Define the Product model


class Product(BaseModel):
    name: str = "test item"
    description: str = "blah blah blah"
    price: float = 0.0
    sku: Optional[int] = None
    image: Optional[str] = "https://i1.wp.com/gelatologia.com/wp-content/uploads/2020/07/placeholder.png"
    quantity: Optional[int] = 1
    created_at: Optional[str] = str(datetime.now())  # Add this line


# Define the home route


@app.get("/")
def home():
    """
    Redirects to the API documentation.
    """
    return "Goto http://0.0.0.0:8000/docs to see the API documentation"

# Define the route to get all products


@app.get("/products/")
async def get_products(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    """
    Retrieves a list of all products, optionally filtered by date range.
    """
    filters = {}
    if start_date:
        filters["created_at"] = {"gte": start_date}
    if end_date:
        filters["created_at"] = {"lte": end_date}

    products = await prisma.product.find_many(where=filters)
    return products
# Define the route to create a product


@app.post("/products/", )
async def create_product(product: Product, background_tasks: BackgroundTasks):
    """
    Creates a new product and adds it to the queue.
    """
    new_product = await prisma.product.create(product.model_dump())
    background_tasks.add_task(push_product_to_queue, new_product.id)
    return new_product

# Define the route to read a product by ID


@app.get("/products/{product_id}", )
async def read_product(product_id: int, q: Union[str, None] = None):
    """
    Retrieves information about a product based on its ID.
    """
    product = await prisma.product.find_unique(where={"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Define the route to update a product by ID


@app.put("/products/{product_id}", )
async def update_product(product_id: int, product: Product):
    """
    Updates an existing product.
    """
    existing_product = await prisma.product.find_unique(where={"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await prisma.product.update(
        where={"id": product_id}, data=product.dict(exclude_unset=True)
    )
    return updated_product

# Define the route to delete a product by ID


@app.delete("/products/{product_id}", )
async def delete_product(product_id: int):
    """
    Deletes a product based on its ID.
    """
    existing_product = await prisma.product.find_unique(where={"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted_product = await prisma.product.delete(where={"id": product_id})
    return deleted_product




# Start a background task to consume the queue
import asyncio
loop = asyncio.get_event_loop()
loop.create_task(consume_product_queue())