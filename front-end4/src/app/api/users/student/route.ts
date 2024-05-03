import { NextApiRequest, NextApiResponse } from 'next';
import mongoose from 'mongoose';
import { connect } from '@/dbConfig/dbConfig'; // Import the connect function
import User from '@/models/userModel'; // Import the User model
import { NextResponse } from "next/server";
import jwt, { JwtPayload } from "jsonwebtoken" // Import JwtPayload interface


connect(); // Call the connect function to establish the database connection

export async function GET(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    try {
      // Extract user ID from JWT token

      const token = req.cookies.get('token').value;
      console.log(token);
      const decoded: JwtPayload = jwt.verify(token, process.env.TOKEN_SECRET!) as JwtPayload;
      const userId = decoded.id;

      // Fetch student data based on logged-in user ID
      const student = await User.findById(userId);

      if (!student) {
        return NextResponse.json({ error: 'Student data not found' }, { status: 404 });
      }

      return NextResponse.json({ student }, { status: 200 });
    } catch (error) {
      console.error(error);
      return NextResponse.json({ error: error }, { status: 500 });
    }
  } else {
    return NextResponse.json({ error: 'Method Not Allowed' }, { status: 405 });
  }
}