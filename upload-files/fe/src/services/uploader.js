// src/services/uploader.js
// A small utility to handle file uploads to the backend.
// Parameters allow configuring file type checking and request content type.

/**
 * Upload a file to the backend.
 * @param {File|Blob} file - File to upload
 * @param {Object} options
 * @param {string} [options.apiUrl] - Base API URL (defaults to import.meta.env.VITE_API_URL)
 * @param {string|string[]} [options.fileType] - Allowed file MIME type(s) or extension(s) used for validation. Examples: 'text/csv', '.csv', ['text/csv', '.csv']
 * @param {string} [options.contentType] - Desired request content type. Default uses multipart/form-data via FormData.
 * @param {number} [options.maxSizeMb=100] - Max file size in MB.
 * @returns {Promise<{ok: boolean, status: number, message: string}>}
 */
export async function uploadFile(file, options = {}) {
  const {
    apiUrl = import.meta.env.VITE_API_URL,
    fileType = ['text/csv', '.csv'],
    contentType, // default undefined => use multipart/form-data
    maxSizeMb = 100,
  } = options;

  if (!file) {
    return { ok: false, status: 0, message: 'No file provided' };
  }

  if (!apiUrl) {
    return { ok: false, status: 0, message: 'VITE_API_URL is not configured.' };
  }

  // Normalize allowed types
  const allowed = Array.isArray(fileType) ? fileType : [fileType];

  // Validate type/extension when possible
  const name = file.name || '';
  const mime = file.type || '';
  const isAllowed = allowed.some((t) => {
    if (!t) return false;
    const tt = String(t).toLowerCase().trim();
    if (tt.startsWith('.')) {
      return name.toLowerCase().endsWith(tt);
    }
    // treat other strings as mime type
    return mime.toLowerCase() === tt;
  });

  if (!isAllowed) {
    return { ok: false, status: 0, message: 'Please upload a valid file of type: ' + allowed.join(', ') };
  }

  // Validate size
  const maxBytes = maxSizeMb * 1024 * 1024;
  if (file.size > maxBytes) {
    return { ok: false, status: 0, message: `File must be smaller than ${maxSizeMb} MB.` };
  }

  try {
    let res;

    if (!contentType || contentType.toLowerCase().includes('multipart/form-data')) {
      // Use FormData; do NOT set Content-Type header manually so browser sets boundary.
      const formData = new FormData();
      formData.append('file', file);
      res = await fetch(apiUrl + '/uploadfile/', {
        method: 'POST',
        body: formData,
      });
    } else {
      // Send raw body with provided content type
      res = await fetch(apiUrl + '/uploadfile/', {
        method: 'POST',
        headers: {
          'Content-Type': contentType,
        },
        body: file,
      });
    }

    let message = '';
    const respType = res.headers.get('content-type') || '';
    if (respType.includes('application/json')) {
      const data = await res.json().catch(() => null);
      message = data ? JSON.stringify(data) : await res.text();
    } else {
      message = await res.text();
    }

    if (!res.ok) {
      return { ok: false, status: res.status, message: message || `Upload failed with status ${res.status}` };
    }

    return { ok: true, status: res.status, message: message || 'Upload successful' };
  } catch (e) {
    return { ok: false, status: 0, message: e?.message || 'Upload failed' };
  }
}
