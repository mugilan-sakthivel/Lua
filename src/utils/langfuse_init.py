"""Langfuse configuration and initialization."""

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env before Langfuse is imported

from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
langfuse_handler = CallbackHandler(public_key=os.getenv("LANGFUSE_PUBLIC_KEY"))
