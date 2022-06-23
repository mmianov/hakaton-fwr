import './Newsletter.css'; 
import Navbar from './Navbar';
import NewsletterBody from './NewsletterBody';

function Newsletter() {
    return (
        <div className="Newsletter">
            <Navbar />
            <NewsletterBody />
        </div>
    );
}

export default Newsletter;