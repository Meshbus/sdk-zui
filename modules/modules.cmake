# SPDX-FileCopyrightText: 2026 FoBE Studio
# SPDX-License-Identifier: Apache-2.0

# Fallback for sdk-heatshrink, which currently uses external Zephyr glue.
# A consuming application may supply its own integration.
if(NOT DEFINED ZEPHYR_HEATSHRINK_CMAKE_DIR)
  set(ZEPHYR_HEATSHRINK_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR}/heatshrink)
  set(ZEPHYR_HEATSHRINK_KCONFIG ${CMAKE_CURRENT_LIST_DIR}/heatshrink/Kconfig)
endif()
