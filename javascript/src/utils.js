import crypto from 'crypto';

export function fingerprintFromHeaders(headers = {}, ip = '') {
  const seed = ip + '::' + (headers['user-agent'] || '');
  return crypto.createHash('sha256').update(seed).digest('hex');
}
