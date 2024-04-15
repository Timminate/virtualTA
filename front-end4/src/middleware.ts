import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname

  // Define paths that are considered public (accessible without a token)
  const isPublicPath = path === '/login' || path === '/signup' || path === '/verifyemail'

  const token = request.cookies.get('token')?.value || ''

  if(isPublicPath && token) {

 // If trying to access a public path with a token, redirect to the home page
    return NextResponse.redirect(new URL('/', request.nextUrl))
  }

// If trying to access a protected path without a token, redirect to the login page
  if (!isPublicPath && !token) {
    return NextResponse.redirect(new URL('/login', request.nextUrl))
  }
    
}


export const config = {
  matcher: [
    '/',
    '/profile',
    '/login',
    '/signup',
    '/verifyemail'
  ]
}