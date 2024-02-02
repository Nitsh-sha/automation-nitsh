import os

# Determine the environment (e.g., 'development' or 'production')
environment = os.getenv('MY_ENVIRONMENT', 'development')

# Define the path to the corresponding requirements file
requirements_file = f'requirements.txt'

# Check if the requirements file exists
if not os.path.exists(requirements_file):
    print(f"Error: {requirements_file} not found.")
    exit(1)

#generate_requirements.py
#  Read the requirements from the environment-specific file
with open(requirements_file, 'r') as file:
    requirements = file.read()

# Write the requirements to a common requirements.txt file
with open('requirements.txt', 'w') as file:
    file.write(requirements)

print(f"Requirements have been generated from {requirements_file} to requirements.txt.")
