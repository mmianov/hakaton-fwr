import Navbar from "../components/Navbar";
import './PageNotFound.css';
import { Link } from "react-router-dom";

const PageNotFound = () => {
    return (
        <div className="PageNotFound">
            <Navbar />
            <div className="error">
                <h2 className="not-found-info">Przepraszamy, ta strona nie istnieje</h2>
                <Link to={'/'} className="home-link">Wróć na stronę główną</Link>
            </div>
        </div>
    );
}
 
export default PageNotFound;