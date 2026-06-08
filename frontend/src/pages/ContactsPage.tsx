import { useEffect, useState } from "react"
import axios from "axios"
import Layout from "../components/Layout"

function ContactsPage() {
  const [contacts, setContacts] = useState<any[]>([])

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [position, setPosition] = useState("")
  const [companyId, setCompanyId] = useState("1")

  const loadContacts = () => {
    const token = localStorage.getItem("token")

    axios
      .get(
        "http://127.0.0.1:8000/contacts",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      .then((response) => {
        setContacts(response.data)
      })
  }

  useEffect(() => {
    loadContacts()
  }, [])

  const createContact = async () => {
    try {
      const token = localStorage.getItem("token")

      await axios.post(
        "http://127.0.0.1:8000/contacts",
        {
          first_name: firstName,
          last_name: lastName,
          email,
          phone,
          position,
          company_id: Number(companyId)
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setFirstName("")
      setLastName("")
      setEmail("")
      setPhone("")
      setPosition("")

      loadContacts()
    } catch (error) {
      console.error(error)
    }
  }

  const deleteContact = async (
    contactId: number
  ) => {
    try {
      const token =
        localStorage.getItem("token")

      await axios.delete(
        `http://127.0.0.1:8000/contacts/${contactId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      loadContacts()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <Layout>
      <div className="container">
        <h1>Contacts</h1>

        <div className="card">
          <div className="form-row">

            <input
              placeholder="First Name"
              value={firstName}
              onChange={(e) =>
                setFirstName(e.target.value)
              }
            />

            <input
              placeholder="Last Name"
              value={lastName}
              onChange={(e) =>
                setLastName(e.target.value)
              }
            />

            <input
              placeholder="Email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
            />

            <input
              placeholder="Phone"
              value={phone}
              onChange={(e) =>
                setPhone(e.target.value)
              }
            />

            <input
              placeholder="Position"
              value={position}
              onChange={(e) =>
                setPosition(e.target.value)
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
              onClick={createContact}
            >
              Create Contact
            </button>

          </div>
        </div>

        <br />

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Position</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {contacts.map((contact) => (
              <tr key={contact.id}>
                <td>{contact.id}</td>
                <td>{contact.first_name}</td>
                <td>{contact.last_name}</td>
                <td>{contact.email}</td>
                <td>{contact.phone}</td>
                <td>{contact.position}</td>

                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() =>
                      deleteContact(contact.id)
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

export default ContactsPage