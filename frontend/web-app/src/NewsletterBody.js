import { useState } from 'react';
import './Newsletter.css';
import axios from 'axios';

function NewsletterBody() {

    let postData = {
        "author": "front-app",
        "token": "c37124596a2761145175c414b6780c8dd93323156d75453cf6617e59a5a45b15",
        "email": ""
    }

    const headers = {
        'Content-Type': 'application/json'
      }

    const [emailInput, setEmailInput] = useState("");
    const [isEmailCorrect, setIsEmailCorrect] = useState(true);
    const [isSent, setIsSent] = useState(false);
    
    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSent(false);
        if (!emailInput.includes("@")) {
            setIsEmailCorrect(false);
        } else {
            setIsEmailCorrect(true);
            postData["email"] = emailInput;
            postRequest();
        }
    }

    const postRequest = () => {
        axios.post(`http://10.10.40.21:5000/subscribe`, postData, {headers: headers}).then(() => 
            setIsSent(true)).catch((e) => 
                console.log(e))
    }

    return (
        <div className='Newsletter-body'>
            <div className='main-container'>
                <div className='form'>
                    <h2>Zapisz się do newslettera!</h2>
                    <p className='info'>Chroń siebie i swoich bliskich będąc na bieżąco! Zapisując się do naszego newslettera, otrzymasz powiadomienia najszybciej, jak to tylko możliwe, żebyś zawsze mógł się czuć bezpiecznie.</p>
                    
                    <form onSubmit={handleSubmit}>
                        <input placeholder='Podaj email' type="text" className='email-input' value={emailInput} onChange={(e) => setEmailInput(e.target.value)}></input>
                        <input className='submit-btn' type="submit" value="Zapisz się"></input>
                    </form>
                    <p className='email-check'>{!isEmailCorrect ? "Proszę wprowadzić poprawny adres email" : (isSent && "Zapisano do newslettera!")}</p>
                    <p className='agreement'>Klikając przycisk „Zapisz się” wyrażasz zgodę na otrzymywanie drogą mailową materiałów informacyjnych przekazywanych przez Cyberly. Możesz w dowolnym czasie cofnąć zgodę na newsletter. W celu rezygnacji z subskrypcji należy skorzystać z linku umieszczonego w każdym newsletterze lub poinformować nas poprzez formularz kontaktowy.</p>
                </div>
            </div>
        </div>
    );
}

export default NewsletterBody;