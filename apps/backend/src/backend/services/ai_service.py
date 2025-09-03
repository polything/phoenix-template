"""
AI Service for LangChain integration.
Provides a simple interface for AI operations using LangChain and LangSmith.
"""

import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langsmith import Client
import asyncio


class AIService:
    """Service for AI operations using LangChain."""
    
    def __init__(
        self, 
        openai_api_key: str, 
        langsmith_api_key: Optional[str] = None,
        langsmith_project: Optional[str] = None,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ):
        """
        Initialize AI service with LangChain and optional LangSmith.
        
        Args:
            openai_api_key: OpenAI API key
            langsmith_api_key: LangSmith API key for tracing (optional)
            langsmith_project: LangSmith project name (optional)
            model_name: Model to use (default: gpt-3.5-turbo)
            temperature: Model temperature (default: 0.7)
        """
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=temperature
        )
        
        # Initialize LangSmith if API key provided
        self.langsmith_enabled = False
        if langsmith_api_key:
            try:
                os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
                os.environ["LANGCHAIN_TRACING_V2"] = "true"
                if langsmith_project:
                    os.environ["LANGCHAIN_PROJECT"] = langsmith_project
                self.langsmith_client = Client()
                self.langsmith_enabled = True
            except Exception as e:
                print(f"Warning: LangSmith initialization failed: {e}")
    
    async def generate_text(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using LangChain.
        
        Args:
            prompt: The prompt to send to the AI
            context: Optional context to include with the prompt
            max_tokens: Optional maximum tokens to generate
            
        Returns:
            Generated text content
        """
        try:
            # Add context to prompt if provided
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                full_prompt = f"Context:\n{context_str}\n\nPrompt: {prompt}"
            else:
                full_prompt = prompt
            
            message = HumanMessage(content=full_prompt)
            
            # Configure model with max_tokens if provided
            if max_tokens:
                self.llm.max_tokens = max_tokens
            
            response = await self.llm.ainvoke([message])
            return response.content
            
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
    
    async def analyze_data(
        self, 
        data: str, 
        analysis_type: str = "summary"
    ) -> str:
        """
        Analyze data using AI.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis (summary, insights, etc.)
            
        Returns:
            Analysis result
        """
        prompt = f"Please provide a {analysis_type} of the following data:\n\n{data}"
        return await self.generate_text(prompt)
    
    async def chat_completion(
        self, 
        messages: list, 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Chat completion with multiple messages.
        
        Args:
            messages: List of message strings
            system_prompt: Optional system prompt
            
        Returns:
            Chat completion response
        """
        try:
            langchain_messages = []
            
            if system_prompt:
                langchain_messages.append(HumanMessage(content=f"System: {system_prompt}"))
            
            for message in messages:
                langchain_messages.append(HumanMessage(content=message))
            
            response = await self.llm.ainvoke(langchain_messages)
            return response.content
            
        except Exception as e:
            raise Exception(f"Chat completion failed: {str(e)}")
    
    def get_langsmith_status(self) -> Dict[str, Any]:
        """Get LangSmith integration status."""
        return {
            "enabled": self.langsmith_enabled,
            "project": os.environ.get("LANGCHAIN_PROJECT", "Not set"),
            "tracing": os.environ.get("LANGCHAIN_TRACING_V2", "false") == "true"
        }


class AIError(Exception):
    """Custom exception for AI service errors."""
    pass
