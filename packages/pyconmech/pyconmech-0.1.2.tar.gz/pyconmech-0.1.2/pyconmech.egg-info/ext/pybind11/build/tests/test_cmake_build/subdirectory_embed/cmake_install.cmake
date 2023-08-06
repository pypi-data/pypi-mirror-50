# Install script for directory: C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/tests/test_cmake_build/subdirectory_embed

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/test_subdirectory_embed")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE STATIC_LIBRARY FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/Debug/test_embed_lib.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE STATIC_LIBRARY FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/Release/test_embed_lib.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE STATIC_LIBRARY FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/MinSizeRel/test_embed_lib.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE STATIC_LIBRARY FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/RelWithDebInfo/test_embed_lib.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake/test_export.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake/test_export.cmake"
         "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake/test_export-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake/test_export.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake" TYPE FILE FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake" TYPE FILE FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export-debug.cmake")
  endif()
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake" TYPE FILE FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export-minsizerel.cmake")
  endif()
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake" TYPE FILE FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export-relwithdebinfo.cmake")
  endif()
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/test_export/test_export-Targets.cmake" TYPE FILE FILES "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/CMakeFiles/Export/lib/cmake/test_export/test_export-Targets.cmake/test_export-release.cmake")
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/pybind11/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "C:/Users/harry/Documents/pb-construction/conmech/ext/pybind11/build/tests/test_cmake_build/subdirectory_embed/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
