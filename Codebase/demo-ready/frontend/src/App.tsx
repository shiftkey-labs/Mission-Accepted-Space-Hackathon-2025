import "./App.css";
import HomePage from "./pages/home";
import { IceExtentProvider } from "./context/IceExtentContext";

const App = () => (
  <IceExtentProvider>
    <HomePage />
  </IceExtentProvider>
);

export default App;
