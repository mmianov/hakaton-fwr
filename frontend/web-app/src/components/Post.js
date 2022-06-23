import './Post.css';

function Post(props) {

    const renderImages = () => {
        return props.data.content_images.map(image => {
            <li>
                <img className='content-image' src={image}/>
            </li>
        })
    }

    return (
        <li key={props.data.id}>
            <div className='post-container'>
                <div className='post-author'>
                    <div className='author-links'>
                        <a className='author-link' href={props.data.author_link} target="_blank"> 
                            <img src={props.data.avatar}/>
                        </a>
                        <a className='author-link' href={props.data.author_link} target="_blank">
                            <h2>{props.data.author}</h2>
                        </a>
                        <a className='author-link' href={props.data.author_link} target="_blank">
                            <p className='username'>{props.data.username}</p>
                        </a>
                    </div>
                    <p className='post-data'>{props.data.date}</p>
                </div>
                <div className='post-content'>
                    <h3>{props.data.content}</h3>
                    <br/>
                    <p>Dowiedz się więcej: </p>
                    <a className='content-link' href={props.data.link} target="_blank">{props.data.link}</a>
                    <ul className='content-images'>{renderImages}</ul>
                </div>
            </div>
        </li>
    );
}

export default Post;