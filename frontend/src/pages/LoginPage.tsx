import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        {
          email,
          password
        }
      )

      console.log(response.data)

      localStorage.setItem(
        "token",
        response.data.access_token
      )

      navigate("/dashboard")
    } catch (error) {
      alert("Invalid credentials")
      console.error(error)
    }
  }

  return (
    <div>
      <h1>Login</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <br />

      <button onClick={handleLogin}>
        Login
      </button>
    </div>
  )
}

export default LoginPage