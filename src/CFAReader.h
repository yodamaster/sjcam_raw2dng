
#ifndef __CFA_READER_H__
#define __CFA_READER_H__

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
typedef unsigned char uint8_t;
#endif

// Color Filter Array reader (read raw sensor readout to byte aligned format)
class CFAReader
{
  public:
  CFAReader();

  int open(const char *fname, size_t expected_size);

  void read(uint8_t *out_buf, size_t total);

  void read(uint8_t *out_buf, size_t x, size_t y, size_t stride);

  ~CFAReader();

  protected:
  uint8_t *m_buf;
#if defined(_WIN32) || defined(_WIN64)
  HANDLE m_fd;
  HANDLE m_map_handle;
#else
  int m_fd;
#endif
  size_t m_filesz;
};

#endif // __CFA_READER_H__
