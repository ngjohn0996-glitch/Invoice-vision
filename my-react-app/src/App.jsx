import {Routes, Route, Link} from "react-router-dom"
import NavDropdown from "./NavDropdown"
import Callback from "./Callback"
import {RefreshProvider} from "./Refresh"
import Component1 from "./Component1"
import Component2 from "./Component2"
import Needauth from "./Needauth"
import NavigateNeedauth from "./NavigateNeedauth"
import {RememberMeProvider} from "./RememberMe"

function App() {

  return(
    <>
      <RefreshProvider>
      <RememberMeProvider>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <NavDropdown/>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Component1/>}/>
          <Route path="/callback" element={<Callback/>}/>
          <Route path="/invoice-automation" element={
            <NavigateNeedauth>
              <Component2/>
            </NavigateNeedauth>}/>
          <Route path="/need-auth" element={<Needauth/>}/>
        </Routes>
      </RememberMeProvider>
      </RefreshProvider>
    </>
  )
}

export default App