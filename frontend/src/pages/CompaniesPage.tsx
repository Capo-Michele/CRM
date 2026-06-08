import { useEffect, useState } from "react"
import axios from "axios"
import Layout from "../components/Layout"

function CompaniesPage() {
  const [companies, setCompanies] = useState<any[]>([])

  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [website, setWebsite] = useState("")
  const [phone, setPhone] = useState("")

  const loadCompanies = () => {
    const token = localStorage.getItem("token")

    axios
      .get(
        "http://127.0.0.1:8000/companies",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      .then((response) => {
        setCompanies(response.data)
      })
  }

  useEffect(() => {
    loadCompanies()
  }, [])

  const createCompany = async () => {
    try {
      const token = localStorage.getItem("token")

      await axios.post(
        "http://127.0.0.1:8000/companies",
        {
          name,
          email,
          website,
          phone
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setName("")
      setEmail("")
      setWebsite("")
      setPhone("")

      loadCompanies()
    } catch (error) {
      console.error(error)
    }
  }

const deleteCompany = async (
companyId: number
) => {
  try {
    const token =
      localStorage.getItem("token")

    await axios.delete(
      `http://127.0.0.1:8000/companies/${companyId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    loadCompanies()
  } catch (error) {
    console.error(error)
  }
}


return (
  <Layout>
    <div className="container">
      <h1>Companies</h1>

      <div className="card">
        <div className="form-row">
          <input
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            placeholder="Website"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
          />

          <input
            placeholder="Phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />

          <button
            className="btn"
            onClick={createCompany}
          >
            Create Company
          </button>
        </div>
      </div>

      <br />

      <table>
        <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Website</th>
            <th>Phone</th>
            <th>Actions</th>
        </tr>
        </thead>

        <tbody>
            {companies.map((company) => (
                <tr key={company.id}>
                <td>{company.id}</td>
                <td>{company.name}</td>
                <td>{company.email}</td>
                <td>{company.website}</td>
                <td>{company.phone}</td>

                <td>
                    <button
                    className="btn btn-danger"
                    onClick={() => deleteCompany(company.id)}
                    >
                    Delete
                    </button>
                </td>
                </tr>
            ))}
        </tbody>    
      </table>
    </div>
  </Layout>
)
}

export default CompaniesPage