import {Card, Col, Container, Row} from "react-bootstrap";

export default function Timeline() {
    return (
        <Container>
            <Row className="mb-5"/>
            <Card>
                <Card.Header>
                    <h2>Hi!</h2>
                </Card.Header>
                <Card.Body>
                    This is a sample card!
                </Card.Body>
            </Card>
        </Container>
    )
}
