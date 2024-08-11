import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, test } from 'vitest'

import App from '../src/App'

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
})
