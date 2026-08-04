document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Datos simulados del Blog (JSON)
    const blogPosts = [
        {
            title: "Arquitectura escalable en Pet Match",
            category: "Arquitectura de Software",
            excerpt: "Análisis sobre la implementación del patrón Repository y la estructura de un proyecto tipo Tinder para adopción de mascotas."
        },
        {
            title: "Desarrollo Full-Stack para sistemas de reserva",
            category: ".NET & Angular",
            excerpt: "Cómo renderizar y gestionar seating plans interactivos para teatros utilizando SQL Server, WebAPI en .NET y Angular."
        },
        {
            title: "Prevención de lesiones en danza con IA",
            category: "Inteligencia Artificial",
            excerpt: "Uso de Teachable Machine de Google para la detección y corrección de postura en profesionales de ballet clásico y contemporáneo."
        },
        {
            title: "Bases de datos en tiempo real con Supabase",
            category: "Vanilla JS",
            excerpt: "Creación de un calendario de citas psicológicas gestionando entidades relacionales directamente desde el cliente con Supabase."
        }
    ];

    // 2. Renderizar los artículos del blog dinámicamente
    const blogGrid = document.getElementById('blog-grid');

    blogPosts.forEach(post => {
        // Crear elemento de tarjeta
        const card = document.createElement('article');
        card.className = 'card';
        
        // Estructura interna de la tarjeta
        card.innerHTML = `
            <span class="tag">${post.category}</span>
            <h3>${post.title}</h3>
            <p>${post.excerpt}</p>
        `;
        
        // Añadir al DOM
        blogGrid.appendChild(card);
    });

    // 3. Manejo del formulario de contacto
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Evitar que la página se recargue

        // Obtener valores de los inputs
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // Aquí iría la lógica para enviar los datos a un backend real o API (ej. EmailJS, Formspree)
        // Por ahora, simulamos un envío exitoso:
        
        formStatus.style.color = '#10B981'; // Color verde de éxito
        formStatus.textContent = `¡Gracias por tu mensaje, ${name}! Me pondré en contacto contigo pronto.`;

        // Limpiar el formulario
        contactForm.reset();

        // Ocultar el mensaje después de 5 segundos
        setTimeout(() => {
            formStatus.textContent = '';
        }, 5000);
    });
});