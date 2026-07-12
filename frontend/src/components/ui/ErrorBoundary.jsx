import { Component } from 'react'
import { Container, Button } from 'react-bootstrap'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <Container className='py-5 text-center'>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🌿</div>
          <h3 style={{ color: '#2d6a4f' }}>یه مشکلی پیش اومد!</h3>
          <p className='text-muted mb-4'>مثل گیاهی که آب ندیده — یه خطای غیرمنتظره رخ داد.</p>
          <Button
            className='btn-aqualotus'
            onClick={() => { this.setState({ hasError: false }); window.location.href = '/' }}
          >
            🏠 برگشت به خانه
          </Button>
        </Container>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
