// Team 16: COMP90024-Assignment2
// Team Members:
// Qingmeng Xu, 969413
// Tingqian Wang, 1043988
// Zhong Liao, 1056020
// Cheng Qian, 962539
// Zongcheng Du, 1096319

const express = require('express')
const path = require('path')
const app = express()

app.use(express.static(path.join(__dirname, 'public')))

app.listen(8080, () => {
  console.log('App listening at port 8080')
})