export const cookieOptions = {
  httpOnly: true,    // Prevents client-side access
  secure: true,      // Only sent over HTTPS
  sameSite: 'none',   // Allow cross-site requests
  path: '/',         // Cookie available for entire site
  maxAge: 3600       // 1 hour expiry
} as const;
