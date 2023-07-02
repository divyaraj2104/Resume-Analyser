const express=require('express')
const app=express()
const cors=require('cors')
const mongoose=require('mongoose')
const User=require('./models/user.model')
const jwt = require('jsonwebtoken')
const bcrypt = require('bcryptjs')





app.use(cors())
app.use(express.json())



const mon_url="mongodb+srv://rct:rct@cluster0.bitig7n.mongodb.net/?retryWrites=true&w=majority"
mongoose.set('strictQuery', true)
mongoose.connect(mon_url)
.then(()=>{
    console.log("mongodb connected");
})
.catch((e)=>{
    console.log(e)
})


// mongoose.connect('mongodb://localhost:27017/resume_analyzer')

app.post('/api/register', async (req, res) => {
	console.log(req.body)
	try {
		const newPassword = await bcrypt.hash(req.body.password, 10)
		await User.create({
			firstName: req.body.firstName,
            lastName: req.body.lastName,
			email: req.body.email,
			password: newPassword,
		})
		res.json({ status: 'ok' })
	} catch (err) {
		res.json({ status: 'error', error: 'Duplicate email' })
	}
})

app.post('/api/login', async (req, res) => {

	try{
		const user = await User.findOne({
			email: req.body.email,
		})
	
		if (!user) {
			return { status: 'error', error: 'Invalid login' }
		}
	
		const isPasswordValid = await bcrypt.compare(
			req.body.password,
			user.password
		)
	
		if (!isPasswordValid) {
			return res.status(400).json({ message: 'Invalid credentials' });
		} 
	
		const token = jwt.sign({ userId: user._id }, 'secret123');
	
		res.status(200).json({ token });	
	}
	catch (err) {
		console.error(err);
		res.status(500).json({ message: 'Server error' });
	  }
	
})

//to get data for displaying user data...
app.get('/api/profile', verifyToken, async (req, res) => {
  try {
    // decode the token to retrieve the user's ID
    const decoded = jwt.verify(req.token, 'secret123');
    const userId = decoded.userId;

    // retrieve the user's information from the database
    const user = await User.findById(userId);

    // return the user's information as a JSON object
    res.json(user);
  } catch (error) {
    res.status(401).json({ message: 'Unauthorized' });
  }
});
  

  function verifyToken(req, res, next) {
	// retrieve the token from the headers
	const bearerHeader = req.headers.authorization;
	if (typeof bearerHeader !== 'undefined') {
	  const bearerToken = bearerHeader.split(' ')[1];
	  req.token = bearerToken;
	  next();
	} else {
	  res.status(401).json({ message: 'Unauthorized' });
	}
  }


  app.put('/api/:id', async (req, res) => {
	try {
	  const { id } = req.params;
	  const { firstName, lastName, email} = req.body;
  
	  const user = await User.findByIdAndUpdate(id, { firstName, lastName, email}, { new: true });
  
	  res.status(200).json(user);
	} catch (err) {
	  console.error(err);
	  res.status(500).json({ error: 'Server error' });
	}
  });




app.listen(1337, () => {
	console.log('Server started on 1337')
})



