# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Copy the local index.html file to the /usr/share/nginx/html directory
COPY index.html /usr/share/nginx/html
COPY favicon.ico /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Command to run when the container starts
CMD ["nginx", "-g", "daemon off;"]
