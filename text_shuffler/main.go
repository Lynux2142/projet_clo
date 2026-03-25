package main

import (
	"math/rand"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func shuffleRunes(runes []rune) {
	rand.Shuffle(len(runes), func(i, j int) {
		runes[i], runes[j] = runes[j], runes[i]
	})
}

func shuffle_text(text string) string {
	lines := strings.Split(text, "\n")

	for i, line := range lines {
		var letters []rune
		for _, r := range line {
			if r != ' ' {
				letters = append(letters, r)
			}
		}

		shuffleRunes(letters)

		resultLine := []rune(line)
		letterIndex := 0
		for j, r := range resultLine {
			if r != ' ' {
				resultLine[j] = letters[letterIndex]
				letterIndex++
			}
		}
		lines[i] = string(resultLine)
	}

	return strings.Join(lines, "\n")
}

func main() {
	a := app.New()
	w := a.NewWindow("Text Shuffler")

	input := widget.NewMultiLineEntry()
	input.Wrapping = fyne.TextWrapWord

	output := widget.NewMultiLineEntry()
	output.Wrapping = fyne.TextWrapWord

	shuffleButton := widget.NewButton("Shuffle Text", func() {
		shuffled := shuffle_text(input.Text)
		output.SetText(shuffled)
	})

	split := container.NewVSplit(input, output)
	split.Offset = 0.5

	content := container.NewBorder(
		widget.NewLabel("Enter text to shuffle:"),
		container.NewCenter(shuffleButton),
		nil,
		nil,
		split,
	)

	w.SetContent(content)
	w.Resize(fyne.NewSize(600, 600))
	w.ShowAndRun()
}
