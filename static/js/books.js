const books = [
  {
    title: "Think and Grow Rich",
    author: "Napoleon Hill",
    img: "img/book1.jpg",
    desc: "A classic self-help book on success and mindset."
  },
  {
    title: "Atomic Habits",
    author: "James Clear",
    img: "img/book2.jpg",
    desc: "How small habits lead to remarkable results."
  },
  {
    title: "The Subtle Art of Not Giving a F*ck",
    author: "Mark Manson",
    img: "img/book3.jpg",
    desc: "A raw guide to living a better, more meaningful life."
  },
  {
    title: "Rich Dad Poor Dad",
    author: "Robert Kiyosaki",
    img: "img/book4.jpg",
    desc: "Understanding wealth and mindset differences."
  }
];

// Display Books
function displayBooks(list) {
  const container = document.getElementById("bookList");
  container.innerHTML = "";

  list.forEach(book => {
    container.innerHTML += `
      <div class="book-card">
        <img src="${book.img}" class="book-img">
        <div>
          <h5>${book.title}</h5>
          <p class="text-muted mb-1">Author: ${book.author}</p>
          <p class="small text-secondary">${book.desc}</p>
        </div>
      </div>
    `;
  });
}

displayBooks(books);

// Search Feature
document.getElementById("search").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = books.filter(book =>
    book.title.toLowerCase().includes(value) ||
    book.author.toLowerCase().includes(value)
  );
  displayBooks(filtered);
});
