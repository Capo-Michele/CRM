import { useEffect, useState } from "react"
import axios from "axios"
import Layout from "../components/Layout"

function DealsPage() {
  const [deals, setDeals] = useState<any[]>([])

  const [title, setTitle] = useState("")
  const [amount, setAmount] = useState("")
  const [companyId, setCompanyId] = useState("1")

  const loadDeals = () => {
    const token = localStorage.getItem("token")

    axios
      .get(
        "http://127.0.0.1:8000/deals",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      .then((response) => {
        setDeals(response.data)
      })
  }

  useEffect(() => {
    loadDeals()
  }, [])

  const createDeal = async () => {
    try {
      const token = localStorage.getItem("token")

      await axios.post(
        "http://127.0.0.1:8000/deals",
        {
          title,
          amount: Number(amount),
          company_id: Number(companyId)
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setTitle("")
      setAmount("")

      loadDeals()
    } catch (error) {
      console.error(error)
    }
  }

  const deleteDeal = async (
    dealId: number
  ) => {
    try {
      const token =
        localStorage.getItem("token")

      await axios.delete(
        `http://127.0.0.1:8000/deals/${dealId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      loadDeals()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <Layout>
      <div className="container">
        <h1>Deals</h1>

        <div className="card">
          <div className="form-row">

            <input
              placeholder="Title"
              value={title}
              onChange={(e) =>
                setTitle(e.target.value)
              }
            />

            <input
              placeholder="Amount"
              value={amount}
              onChange={(e) =>
                setAmount(e.target.value)
              }
            />

            <input
              placeholder="Company ID"
              value={companyId}
              onChange={(e) =>
                setCompanyId(e.target.value)
              }
            />

            <button
              className="btn"
              onClick={createDeal}
            >
              Create Deal
            </button>

          </div>
        </div>

        <br />

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Company</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {deals.map((deal) => (
              <tr key={deal.id}>
                <td>{deal.id}</td>
                <td>{deal.title}</td>
                <td>${deal.amount}</td>
                <td>{deal.status}</td>
                <td>{deal.company_id}</td>

                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() =>
                      deleteDeal(deal.id)
                    }
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

export default DealsPage