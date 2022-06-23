import './Navbar.css';
import { Link } from "react-router-dom";

function Navbar() {
    return (
        <div className="Navbar">
            <div className="container">
                <a href='/'>
                    <div className='logo'>
                        Cyber<span>ly</span>
                    </div>
                </a>
                <div className='links-container'>
                    <Link to='/alerts'>Alerty</Link>
                    <Link to='/newsletter'>Bądź na bieżąco</Link>
                    <Link to='/developer'>Dla developerów</Link>
                    <Link to='/contact'>Kontakt</Link>
                </div>
            </div>
        </div>
    );
}

export default Navbar;