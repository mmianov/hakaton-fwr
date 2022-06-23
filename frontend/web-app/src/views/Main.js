import './Main.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import Post from '../components/Post';
import Spinner from 'react-bootstrap/Spinner';
import React from "react";

function Main() {

    const [data, setData] = useState([]);
    const [tempData, setTempData] = useState([]);
    const [postsList, setPostsList] = useState();
    const [filterInput, setFilterInput] = useState("");

    useEffect(() => {
        axios.get(`http://10.10.40.21:5000/alerts`)
            .then(res => {
                setData(res.data);
        })
    }, [])

    useEffect(() => {
        setTempData(data);
    }, [data])

    useEffect(() => {
        setPostsList(renderPosts);
    }, [tempData])

    useEffect(() => {
        setTempData(prev => {
            if(filterInput!=="") {
                return prev.filter(el => el.content.toLowerCase().includes(filterInput.toLowerCase()) || el.author.toLowerCase().includes(filterInput.toLowerCase()));
            } else {
                return data;
            }
        })
    }, [filterInput])

    const renderPosts = () => {
        const result = tempData.map((postData) => <Post key={postData.id} data={postData} />);
        sortBy(result, "date");
        return result;
    }

    const compare = (a, b) => {
        return formatDate(b.props.data.date)-formatDate(a.props.data.date);
    }
    
    const formatDate = (stringDate) => {
        const splitted = stringDate.split("/");
        return new Date(splitted[2]+'-'+splitted[1]+'-'+splitted[0]);
    }
    
    const sortBy = (posts, by) => {
        if(!by) {
            return posts;
        } else {
            return posts.sort(compare)
        }
    }

    return (
        <div className={data.length ? 'Main' : 'Main loading'}>
            {data.length!==0 && <div className='filter'>
                <input className='search-bar' type="text" placeholder='Szukaj...' value={filterInput} onChange={(e) => {setFilterInput(e.target.value)}}/>
            </div>}
            <div className='api-output'>{data.length ? <ul>{postsList}</ul> : <Spinner animation="border" />}</div>
        </div>
    );
}

export default Main;