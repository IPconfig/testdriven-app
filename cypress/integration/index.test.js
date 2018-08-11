describe('Index', () => {

    it('should display the page correctly if a user is not logged in', () => {
  
      cy
        .visit('/')
        .get('h1').contains('All Users')
    });
});