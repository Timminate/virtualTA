import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
    email:{
        type: String,
        required: [true, "Please provide email"],
        unique:true
    },
    password:{
        type: String,
        required: [true, "Please provide a password"],
    },
    forgotPasswordToken: String,
    forgotPasswordTokenExpiry: Date,
    verifyToken: String,
    verifyTokenExpiry: Date,
}, 
{
    timestamps: true
})

const User = mongoose.models.User || mongoose.model('User',userSchema);

export default User;