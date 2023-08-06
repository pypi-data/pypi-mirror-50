// Copyright 2019 Global Phasing Ltd.
//
// gemmi::concat()

#ifndef GEMMI_CONCAT_HPP_
#define GEMMI_CONCAT_HPP_

#include <sstream>
#include <string>

namespace gemmi {

template<typename T, typename... Args>
inline void put_into_stream(std::ostringstream&) {}

template<typename T, typename... Args>
void put_into_stream(std::ostringstream& os, T&& value, Args&&... args) {
  os << std::forward<T>(value);
  put_into_stream(os, std::forward<Args>(args)...);
}

template<typename T, typename... Args>
std::string concat(T&& value, Args&&... args) {
  std::ostringstream os;
  put_into_stream(os, std::forward<T>(value), std::forward<Args>(args)...);
  return os.str();
}

} // namespace gemmi
#endif
