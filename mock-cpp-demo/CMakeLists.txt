cmake_minimum_required(VERSION 3.16)
project(CAESolverDemo VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ── Options ──────────────────────────────────────────────────────
option(ENABLE_OPENMP "Enable OpenMP parallel solver loops" ON)
option(ENABLE_TESTS  "Build unit and integration tests"    ON)
option(ENABLE_GUI    "Build Qt-based GUI (requires Qt5)"   OFF)

# ── OpenMP ───────────────────────────────────────────────────────
if(ENABLE_OPENMP)
    find_package(OpenMP)
    if(OpenMP_CXX_FOUND)
        message(STATUS "OpenMP found — parallel solver enabled")
    else()
        message(WARNING "OpenMP not found — solver will run single-threaded")
    endif()
endif()

# ── Include directories ─────────────────────────────────────────
include_directories(${CMAKE_SOURCE_DIR}/include)

# ── Source files ─────────────────────────────────────────────────
set(SOLVER_SOURCES
    src/solver/FEASolver.cpp
    src/solver/SparseMatrix.cpp
)

set(MESH_SOURCES
    src/mesh/MeshGenerator.cpp
    src/mesh/MeshRefinement.cpp
)

set(UTIL_SOURCES
    src/utils/MathUtils.cpp
    src/utils/Logger.cpp
)

set(IO_SOURCES
    src/io/ModelReader.cpp
)

# ── Libraries ────────────────────────────────────────────────────
add_library(cae_solver STATIC ${SOLVER_SOURCES})
add_library(cae_mesh   STATIC ${MESH_SOURCES})
add_library(cae_utils  STATIC ${UTIL_SOURCES})
add_library(cae_io     STATIC ${IO_SOURCES})

target_link_libraries(cae_solver PUBLIC cae_utils)
target_link_libraries(cae_mesh   PUBLIC cae_utils)
target_link_libraries(cae_io     PUBLIC cae_utils)

if(OpenMP_CXX_FOUND)
    target_link_libraries(cae_solver PUBLIC OpenMP::OpenMP_CXX)
endif()

# ── Main executable ──────────────────────────────────────────────
add_executable(cae_demo src/main.cpp)
target_link_libraries(cae_demo PRIVATE cae_solver cae_mesh cae_io cae_utils)

# ── Tests ────────────────────────────────────────────────────────
if(ENABLE_TESTS)
    enable_testing()
    
    add_executable(test_solver tests/unit/test_solver.cpp)
    target_link_libraries(test_solver PRIVATE cae_solver cae_mesh cae_utils)
    add_test(NAME SolverTests COMMAND test_solver)
    
    add_executable(test_mesh tests/unit/test_mesh.cpp)
    target_link_libraries(test_mesh PRIVATE cae_mesh cae_utils)
    add_test(NAME MeshTests COMMAND test_mesh)
    
    add_executable(test_pipeline tests/integration/test_pipeline.cpp)
    target_link_libraries(test_pipeline PRIVATE cae_solver cae_mesh cae_io cae_utils)
    add_test(NAME PipelineTests COMMAND test_pipeline)
endif()

# ── Install ──────────────────────────────────────────────────────
install(TARGETS cae_demo DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
