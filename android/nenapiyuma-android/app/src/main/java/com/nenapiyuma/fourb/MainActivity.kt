package com.nenapiyuma.fourb
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
class MainActivity:ComponentActivity(){
 override fun onCreate(b:Bundle?){super.onCreate(b);setContent{
  MaterialTheme{var p by remember{mutableStateOf("")};var o by remember{mutableStateOf("Local GGUF + native llama.cpp backend required.")}}
  Column(Modifier.fillMaxSize().padding(20.dp)){Text("Nenapiyuma 4B",style=MaterialTheme.typography.headlineMedium)
   OutlinedTextField(p,{p=it},Modifier.fillMaxWidth(),label={Text("Prompt")})
   Button(onClick={o="Offline native backend is required for real inference."}){Text("Run Offline")}
   Text(o)}
 }}
}
