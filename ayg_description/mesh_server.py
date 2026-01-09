#!/usr/bin/env python3
"""
Simple HTTP server for serving robot mesh files.
This allows client applications to access mesh files via HTTP URLs.
"""

import os
import http.server
import socketserver
from pathlib import Path

from ament_index_python.packages import get_package_share_directory


class MeshHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler that serves files from ROS package directories."""
    
    def __init__(self, *args, mesh_base_path=None, **kwargs):
        # Default to ayg_description/meshes if not provided
        if mesh_base_path is None:
            try:
                package_dir = get_package_share_directory('ayg_description')
                mesh_base_path = os.path.join(package_dir, 'meshes')
            except:
                mesh_base_path = None
        self.mesh_base_path = mesh_base_path
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        # Parse the path
        path = self.path.split('?')[0]
        
        # If path starts with '/meshes/', serve it from mesh_base_path
        if path.startswith('/meshes/'):
            if not self.mesh_base_path:
                self.send_error(404, "Mesh base path not configured")
                return
            
            mesh_file = path.replace('/meshes/', '')
            mesh_path = os.path.join(self.mesh_base_path, mesh_file)
            
            # If we found the file, serve it
            if os.path.exists(mesh_path):
                try:
                    with open(mesh_path, 'rb') as f:
                        content = f.read()
                    
                    # Determine content type
                    content_type = 'application/octet-stream'
                    if mesh_file.lower().endswith('.stl'):
                        content_type = 'model/stl'
                    elif mesh_file.lower().endswith('.dae'):
                        content_type = 'model/vnd.collada+xml'
                    elif mesh_file.lower().endswith('.obj'):
                        content_type = 'model/obj'
                    
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.send_header('Content-length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_error(500, f"Error reading file: {str(e)}")
                    return
        
        # Fall back to 404 for other paths
        self.send_error(404, "File not found")
    
    def end_headers(self):
        """Add CORS headers to allow cross-origin requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.end_headers()


def create_mesh_server(port=8080, mesh_base_path=None):
    """
    Create and start an HTTP server for serving mesh files.
    
    Args:
        port: Port number to listen on (default: 8080)
        mesh_base_path: Base path for mesh files (optional, defaults to ayg_description/meshes)
    """
    
    handler = lambda *args, **kwargs: MeshHTTPRequestHandler(
        *args, mesh_base_path=mesh_base_path, **kwargs
    )
    
    class _ThreadingReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        # Allow quick restarts without "Address already in use" due to TIME_WAIT.
        allow_reuse_address = True
        daemon_threads = True

    try:
        httpd = _ThreadingReusableTCPServer(("", port), handler)
    except OSError as e:
        if getattr(e, "errno", None) == 98:
            print(
                f"Port {port} is already in use. "
                f"Stop the existing process or choose a different --port."
            )
        raise

    with httpd:
        print(f"Mesh server started on port {port}")
        if mesh_base_path:
            print(f"Serving meshes from: {mesh_base_path}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down mesh server...")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='HTTP server for robot mesh files')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')
    parser.add_argument('--mesh-path', type=str, default=None,
                        help='Base path for mesh files (optional)')
    
    # When launched via `launch_ros.actions.Node`, ROS 2 may append `--ros-args ...`.
    # This script isn't a ROS node, so tolerate and ignore unknown args.
    args, _unknown = parser.parse_known_args()
    
    create_mesh_server(port=args.port, mesh_base_path=args.mesh_path)


if __name__ == '__main__':
    main()
