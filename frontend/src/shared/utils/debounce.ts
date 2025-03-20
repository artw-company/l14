export const debounce = <T extends (...args: unknown[]) => unknown>(callback: T, ms = 200) => {
  let timeout: ReturnType<typeof setTimeout> | null = null;

  return (...args: Parameters<T>) => {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => {
      callback(...args);
    }, ms);
  };
};
