# =========================== Project Configuration ============================

cmake_minimum_required(VERSION 3.8)
project(ayg_description)

# Default to C99
if(NOT CMAKE_C_STANDARD)
    set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# =============================== Dependencies =================================

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# ================================== Install ===================================

install(DIRECTORY config launch meshes urdf DESTINATION share/${PROJECT_NAME})

# Install the mesh server as a ROS 2 executable (libexec) so `launch_ros.actions.Node`
# can run it as `executable="mesh_server"`.
install(
  PROGRAMS scripts/mesh_server.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME mesh_server
)

# ==============================================================================

ament_package()
