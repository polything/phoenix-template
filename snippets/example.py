# Phoenix Template - Example Code Snippets
# This file contains example code snippets for common patterns

# FastAPI Example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}

# Next.js Example
"""
// Example React component
import { useState } from 'react';

export default function ExampleComponent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
"""
