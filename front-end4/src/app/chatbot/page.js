'use client'
import React from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';
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

  const handleLogout = () => {
    /*
    *
    * Insert logic for logging user out
    * 
    */
    // temp testing log
    console.log('User logged out');
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
          <MDBCol md="8" lg="6" xl="4">
            <MDBCard id="chat1" style={{ borderRadius: '15px' }}>
              <MDBCardHeader
                className="d-flex justify-content-between align-items-center p-3 bg-info text-white border-bottom-0"
                style={{
                  borderTopLeftRadius: '15px',
                  borderTopRightRadius: '15px',
                }}
              >
                <MDBIcon fas icon="angle-left" />
                <p className="mb-0 fw-bold">Live chat</p>
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
                      Hello and thank you for visiting MDBootstrap. Please click
                      the video below.
                    </p>
                  </div>
                </div>

                <div className="d-flex flex-row justify-content-end mb-4">
                  <div
                    className="p-3 me-3 border"
                    style={{ borderRadius: '15px', backgroundColor: '#fbfbfb' }}
                  >
                    <p className="small mb-0">
                      Thank you, I really like your product.
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
                      <img
                        src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/screenshot1.webp"
                        style={{ borderRadius: '15px' }}
                        alt="video"
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
                    <p className="small mb-0">...</p>
                  </div>
                </div>

                <MDBTextArea
                  className="form-outline"
                  label="Type your message"
                  id="textAreaExample"
                  rows={4}
                />
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </div>
  );
}