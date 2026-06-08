import { Link, useNavigate } from "react-router-dom"

function Layout({
  children
}: {
  children: React.ReactNode
}) {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/")
  }
  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh"
      }}
    >
      <aside
        style={{
          width: "220px",
          background: "#1e293b",
          color: "white",
          padding: "20px"
        }}
      >
        <h2>CRM</h2>

        <nav>
          <p>
            <Link
              to="/dashboard"
              style={{ color: "white" }}
            >
              Dashboard
            </Link>
          </p>

          <p>
            <Link
              to="/companies"
              style={{ color: "white" }}
            >
              Companies
            </Link>
          </p>

          <p>
            <Link
              to="/contacts"
              style={{ color: "white" }}
            >
              Contacts
            </Link>
          </p>

          <p>
            <Link
              to="/deals"
              style={{ color: "white" }}
            >
              Deals
            </Link>
          </p>

          
          <p>
            <button
              className="btn btn-danger"
              onClick={logout}
            >
              Logout
            </button>
          </p>
        </nav>
      </aside>

      <main
        style={{
          flex: 1,
          padding: "30px"
        }}
      >
        {children}
      </main>
    </div>
  )
}

export default Layout