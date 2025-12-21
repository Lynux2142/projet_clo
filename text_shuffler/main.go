package main

import (
	"math/rand"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func shuffle_text(text string) string {
	var letters []rune
	for _, r := range text {
		if r != ' ' && r != '\n' {
			letters = append(letters, r)
		}
	}

	rand.Shuffle(len(letters), func(i, j int) {
		letters[i], letters[j] = letters[j], letters[i]
	})

	result := make([]rune, 0, len(text))
	letterIndex := 0

	for _, r := range text {
		if r == ' ' || r == '\n' {
			result = append(result, r)
		} else {
			result = append(result, letters[letterIndex])
			letterIndex++
		}
	}

	return string(result)
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
