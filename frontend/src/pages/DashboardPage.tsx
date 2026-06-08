import { useEffect, useState } from "react"
import axios from "axios"
import Layout from "../components/Layout"

function DashboardPage() {
  const [stats, setStats] = useState<any>(null)
  const [pipeline, setPipeline] = useState<any>(null)

  useEffect(() => {
  const token = localStorage.getItem("token")

  axios
    .get(
      "http://127.0.0.1:8000/dashboard/stats",
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    .then((response) => {
      setStats(response.data)
    })

  axios
    .get(
      "http://127.0.0.1:8000/dashboard/pipeline",
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    .then((response) => {
      setPipeline(response.data)
    })
}, [])

  if (!stats) {
    return (
      <Layout>
        <h1>Loading...</h1>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="container">
        <h1>CRM Dashboard</h1>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "20px"
          }}
        >
          <div className="card">
            <h2>Companies</h2>
            <h1>{stats.companies}</h1>
          </div>

          <div className="card">
            <h2>Contacts</h2>
            <h1>{stats.contacts}</h1>
          </div>

          <div className="card">
            <h2>Deals</h2>
            <h1>{stats.deals}</h1>
          </div>

          <div className="card">
            <h2>Revenue</h2>
            <h1>${stats.revenue}</h1>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default DashboardPage