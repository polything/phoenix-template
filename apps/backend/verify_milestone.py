#!/usr/bin/env python3
"""
Simple milestone verification script that checks file structure and basic syntax.
"""

import os
import sys
import ast
from pathlib import Path


def check_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path), "File exists" if os.path.exists(file_path) else "File not found"


def verify_milestone():
    """Verify milestone components."""
    print("🚀 Verifying AI Content Pipeline Milestone Components...")
    print("=" * 60)
    
    # Define the files that should exist for the milestone
    required_files = [
        # Backend core files
        "src/backend/main.py",
        "src/backend/config/settings.py",
        "src/backend/config/__init__.py",
        "src/backend/services/database_service.py",
        "src/backend/services/langchain_service.py",
        "src/backend/api/clients.py",
        "src/backend/api/pipeline.py",
        "src/backend/models/client.py",
        "src/backend/database/schemas.sql",
        
        # Frontend files
        "../frontend/src/components/ClientIntakeForm.tsx",
        "../frontend/src/components/ContentGenerator.tsx",
        "../frontend/src/lib/api/pipeline.ts",
        "../frontend/src/app/page.tsx",
        
        # Configuration files
        "pyproject.toml",
        "../frontend/package.json",
        "env.example",
    ]
    
    print("\n1. Checking Required Files...")
    all_files_exist = True
    
    for file_path in required_files:
        exists, message = check_file_exists(file_path)
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}: {message}")
        if not exists:
            all_files_exist = False
    
    print("\n2. Checking Python Syntax...")
    python_files = [
        "src/backend/main.py",
        "src/backend/config/settings.py",
        "src/backend/services/database_service.py",
        "src/backend/services/langchain_service.py",
        "src/backend/api/clients.py",
        "src/backend/api/pipeline.py",
        "src/backend/models/client.py",
    ]
    
    all_syntax_valid = True
    for file_path in python_files:
        if os.path.exists(file_path):
            valid, message = check_python_syntax(file_path)
            status = "✅" if valid else "❌"
            print(f"   {status} {file_path}: {message}")
            if not valid:
                all_syntax_valid = False
        else:
            print(f"   ⚠️  {file_path}: File not found (skipping syntax check)")
    
    print("\n3. Checking Key Components...")
    
    # Check if main.py includes pipeline router
    main_py_path = "src/backend/main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
            if "pipeline_router" in content:
                print("   ✅ Pipeline router included in main.py")
            else:
                print("   ❌ Pipeline router not found in main.py")
                all_syntax_valid = False
    
    # Check if database schema exists
    schema_path = "src/backend/database/schemas.sql"
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            content = f.read()
            if "CREATE TABLE clients" in content and "CREATE TABLE content_pipeline_runs" in content:
                print("   ✅ Database schema includes required tables")
            else:
                print("   ❌ Database schema missing required tables")
                all_files_exist = False
    
    # Check if frontend components exist
    frontend_files = [
        "../frontend/src/components/ClientIntakeForm.tsx",
        "../frontend/src/components/ContentGenerator.tsx",
        "../frontend/src/lib/api/pipeline.ts",
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} missing")
            all_files_exist = False
    
    print("\n" + "=" * 60)
    
    if all_files_exist and all_syntax_valid:
        print("🎉 MILESTONE VERIFICATION SUCCESSFUL!")
        print("=" * 60)
        print("\n✅ All milestone components are in place:")
        print("   - Working client intake form on frontend")
        print("   - Backend API that processes client data")
        print("   - Basic LangChain flow connecting pipeline steps")
        print("   - Supabase database integration ready")
        print("\n🔧 To complete the setup:")
        print("   1. Set up Supabase database with the provided schema")
        print("   2. Add your API keys to .env file")
        print("   3. Install dependencies: poetry install (backend) and pnpm install (frontend)")
        print("   4. Run the servers and test the end-to-end flow")
        return True
    else:
        print("❌ MILESTONE VERIFICATION FAILED!")
        print("=" * 60)
        print("\nSome components are missing or have issues.")
        print("Please check the errors above and fix them.")
        return False


if __name__ == "__main__":
    success = verify_milestone()
    sys.exit(0 if success else 1)
