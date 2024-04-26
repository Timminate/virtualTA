'use client'
import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';
import {useRouter} from "next/navigation";
import axios from 'axios';
import { useState } from 'react';
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardHeader,
  MDBCardBody,
  MDBIcon,
  MDBTextArea,
} from 'mdb-react-ui-kit';

export default function ChatBot() {
  const router = useRouter();
  const [name, setName] = useState("");


  const handleSubmit = (event) => {
    event.preventDefault();
    alert(name)
  }

  const handleLogout = async () => {
    try {
      await axios.get('/api/users/logout');
      router.push('/login')
    } catch (error) {
        console.log(error.message)
        
    }
  };

  return (
    <div>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="/chatbot">Virtual TA</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/chatbot">Home</Nav.Link>
              <Nav.Link href="/profile">Profile</Nav.Link>
            </Nav>
            <div className="ms-auto">
              <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
            </div>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <MDBContainer className="py-5">
        <MDBRow className="d-flex justify-content-center">
          <MDBCol md="16" lg="12" xl="8">
            <MDBCard id="chat1" style={{ borderRadius: '15px' }}>
              <MDBCardHeader
                className="d-flex justify-content-between align-items-center p-3 bg-info text-white border-bottom-0"
                style={{
                  borderTopLeftRadius: '15px',
                  borderTopRightRadius: '15px',
                }}
              >
                <MDBIcon fas icon="angle-left" />
                <p className="mb-0 fw-bold">Virtual TA</p>
                <MDBIcon fas icon="times" />
              </MDBCardHeader>

              <MDBCardBody>
                <div className="d-flex flex-row justify-content-start mb-4">
                  <img
                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                    alt="avatar 1"
                    style={{ width: '45px', height: '100%' }}
                  />
                  <div
                    className="p-3 ms-3"
                    style={{
                      borderRadius: '15px',
                      backgroundColor: 'rgba(57, 192, 237,.2)',
                    }}
                  >
                    <p className="small mb-0">
                      What is hashing and hashmap? 
                    </p>
                  </div>
                </div>

                <div className="d-flex flex-row justify-content-end mb-4">
                  <div
                    className="p-3 me-3 border"
                    style={{ borderRadius: '15px', backgroundColor: '#fbfbfb' }}
                  >
                    <p className="small mb-0">
                      At this point you should be familiar with the "Map" interface and the "HashMap" implementation provided by Java. And by making your own "Map" using a hash table, you should understand how "HashMap" works and why we expect its core methods to be constant time. Because of this performance, "HashMap" is widely used, but it is not the only implementation of "Map". There are a few reasons you might want another implementation: Hashing can be slow, so even though "HashMap" operations are constant time, the "constant" might be big.
                      Hashing works well if the hash function distributes the keys evenly among the sub-maps. But designing good hash functions is not easy, and if too many keys end up in the same sub-map, the performance of the "HashMap" may be poor.
                      The keys in a hash table are not stored in any particular order; in fact, the order might change when the table grows and the keys are rehashed. For some applications, it is necessary, or at least useful, to keep the keys in order.
                      It is hard to solve all of these problems at the same time, but Java provides an implementation called "TreeMap" that comes close: 
                      It doesn't use a hash function, so it avoids the cost of hashing and the difficulty of choosing a hash function. - Inside the "TreeMap", the keys are are stored in a binary search tree, which makes it possible to traverse the keys, in order, in linear time.
                      The runtime of the core methods is proportional to log n, which is not quite as good as constant time, but it is still very good.
                      In the next section, I'll explain how binary search trees work and then you will use one to implement a "Map". Along the way, we'll analyze the performance of the core map methods when implemented using a tree.  
                    </p>
                  </div>
                  <img
                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
                    alt="avatar 1"
                    style={{ width: '45px', height: '100%' }}
                  />
                </div>

                <div className="d-flex flex-row justify-content-start mb-4">
                  <img
                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                    alt="avatar 1"
                    style={{ width: '45px', height: '100%' }}
                  />
                  <div className="ms-3" style={{ borderRadius: '15px' }}>
                    <div className="bg-image">
                      <img /*
                        src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/screenshot1.webp"
                        style={{ borderRadius: '15px' }}
                        alt="video" */
                      />
                      <a href="#!">
                        <div className="mask"></div>
                      </a>
                    </div>
                  </div>
                </div>

                <div className="d-flex flex-row justify-content-start mb-4">
                  <img 
                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                    alt="avatar 1"
                    style={{ width: '45px', height: '100%' }} 
                  />
                  <div
                    className="p-3 ms-3"
                    style={{
                      borderRadius: '15px',
                      backgroundColor: 'rgba(57, 192, 237,.2)',
                    }}
                  >
                    <p className="small mb-0">Thank you!</p>
                  </div>
                </div>
                
                <form onSubmit={handleSubmit}>
                  <div>Chat with the Bot</div>
                  <input type= "text" value={name} onChange={(e) => setName(e.target.value)} size="80"/>
                  <input type= "submit" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4"/>
                </form>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </div>
  );
}
