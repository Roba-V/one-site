import { fireEvent, render, screen } from '@testing-library/react'
import axios from 'axios'
import { beforeEach, describe, expect, Mocked, test, vi } from 'vitest'

import App from '../src/App'

vi.mock('axios')

beforeEach(() => {
  const mockedAxios = axios as Mocked<typeof axios>
  mockedAxios.get.mockResolvedValue({
    data: {
      message: 'Hello, World!',
    },
  })
})

describe('IncreaseButton', () => {
  test('renders', () => {
    render(<App />)
    expect(screen.getByText('abc')).toBeDefined()
  })

  test('click', () => {
    const { getByText } = render(<App />)
    expect(screen.getByText('count is 0')).toBeDefined()

    const button = getByText('count is 0')

    fireEvent.click(button)
    expect(screen.getByText('count is 1')).toBeDefined()
  })

  test('get api', () => {
    render(<App />)
  })
})
